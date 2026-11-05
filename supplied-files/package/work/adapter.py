"""Deterministic, read-only adapter for the two supplied-source dossiers.

No external material, inference by entity name, or arithmetic is introduced here.
Dependencies are typed evidence edges; entity and related-assertion identifiers are
metadata references, not permission to import their other sources into a lane.
"""
from __future__ import annotations

import copy
import csv
import hashlib
import io
import json
from pathlib import Path
import re

BASELINE_COMMIT = '40e77bd1e57c0fce62a3a962d977c05b54724e8a'
PHASE = Path('analysis/bleich-profile-financial/data')
LANES = ('scout', 'opeh')
ACCEPTANCE = {'profile_assertions':47,'findings':26,'calculations':129,
              'profile_financial_links':42,'discrepancies':40}
# Lane exports are byte-for-byte record aliases of these authoritative collections.
ALIASES = {'obligations-scout', 'obligations-opeh'}
DEPENDENCY_FIELDS = {
    'supporting_record_ids', 'normalized_fact_ids', 'normalized_fact_id',
    'calculation_ids', 'source_record_id', 'date_basis_record_ids',
    'term_normalized_fact_ids', 'principal_normalized_fact_ids',
    'principal_normalized_fact_id', 'rate_normalized_fact_ids',
    'economic_principal_normalized_fact_id', 'regular_rate_normalized_fact_id',
    'regular_basis_normalized_fact_id', 'default_rate_normalized_fact_id',
    'default_basis_normalized_fact_id', 'election_normalized_fact_id',
    'sanction_normalized_fact_id', 'related_normalized_fact_ids',
    'financial_source_record_ids', 'instrument_ids', 'instrument_id', 'family_id',
    'mention_id', 'source_mention_ids', 'profile_assertion_id', 'financial_finding_id',
}
METADATA_FIELDS = {'entity_id','counterparty_id','obligation_id','candidate_entity_ids',
                   'maker_entity_ids','guarantor_entity_ids','creditor_entity_id',
                   'financial_finding_ids','related_profile_assertion_id'}
CITATION = re.compile(r'^doc:([0-9a-f]{64})#(page|row|line|section)=(.+)$')
SECONDARY_TYPES = {'unattributed_secondary_advocacy_narrative','secondary_research_synthesis'}
PERIPHERAL_TYPES = {'search_index','reference_placeholder','unexecuted_draft',
                    'incomplete_text_derivative','summons_transcription'}


def _read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding='utf-8').splitlines() if line.strip()]


def _dump(path: Path, value: object) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2)+'\n', encoding='utf-8')


def _input_files(repo_root: Path) -> list[Path]:
    return sorted(p for name in ('corpus','analysis') for p in (repo_root/name).rglob('*') if p.is_file())


def _digest(path: Path) -> str:
    digest=hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda:handle.read(1024*1024), b''):digest.update(chunk)
    return digest.hexdigest()


def freeze_inputs(repo_root: Path, output: Path) -> dict:
    """Freeze every original corpus/ and analysis/ file, without touching inputs."""
    repo_root=Path(repo_root)
    manifest={'baseline_commit':BASELINE_COMMIT,'algorithm':'sha256',
              'files':{str(p.relative_to(repo_root)):{'sha256':_digest(p),'size':p.stat().st_size}
                       for p in _input_files(repo_root)}}
    _dump(Path(output),manifest)
    return manifest


def verify_inputs(repo_root: Path, manifest: dict) -> None:
    """Reject changed bytes and added or missing baseline files."""
    repo_root=Path(repo_root)
    actual={str(p.relative_to(repo_root)):p for p in _input_files(repo_root)}
    frozen=manifest['files']
    if set(actual)!=set(frozen):
        raise ValueError(f"input file set changed; added={sorted(set(actual)-set(frozen))}; missing={sorted(set(frozen)-set(actual))}")
    for relative,path in actual.items():
        if path.stat().st_size!=frozen[relative]['size'] or _digest(path)!=frozen[relative]['sha256']:
            raise ValueError(f'input hash changed: {relative}')


def _source_lane(occurrence: dict, containers: dict) -> str:
    container=containers.get(occurrence['container_id'])
    if container:
        if container['name']=='Scout Trading.zip':return 'scout'
        if container['name'].startswith('OPEH LLC Litigation-'):return 'opeh'
        raise ValueError(f"unapproved source container: {container['name']}")
    # The only supplied standalone source belongs to Scout's regulatory lane.
    if occurrence['name']=='Nasdaq $3 mm fine to Bleich.pdf':return 'scout'
    raise ValueError(f"unallocated standalone source: {occurrence['name']}")


def _lanes(record: dict, documents: dict) -> set[str]:
    result=set()
    for citation in record.get('source_citations',[]):
        match=CITATION.fullmatch(citation)
        if not match or match[1] not in documents:raise ValueError(f'invalid source citation: {citation}')
        result.add(documents[match[1]]['dossier_id'])
    if not result:raise ValueError(f"missing source citation: {record.get('id')}")
    return result


def _strings(value) -> list[str]:
    if isinstance(value,str):return [value]
    if isinstance(value,list):return [item for item in value if isinstance(item,str)]
    return []


def _dependency_edges(record: dict) -> list[tuple[str,str]]:
    edges=[]
    for key in sorted(DEPENDENCY_FIELDS):
        edges.extend((key,value) for value in _strings(record.get(key)))
    if isinstance(record.get('operands'),dict):
        edges.extend(('operands',value) for value in record['operands'].values() if isinstance(value,str))
    if record.get('comparison_basis')=='normalized_source':edges.append(('comparison_target',record['comparison_target']))
    return sorted(set(edges))


def build_index(repo_root: Path) -> dict:
    """Allocate sources by supplied archive provenance, then close typed evidence."""
    repo_root=Path(repo_root)
    manifest=json.loads((repo_root/'corpus/manifest.json').read_text(encoding='utf-8'))
    containers={row['id']:row for row in manifest['containers']}
    occurrences=[dict(row,dossier_id=_source_lane(row,containers)) for row in manifest['occurrences']]
    classifications={row['document_id']:row for row in _read_jsonl(repo_root/'corpus/analysis/documents.jsonl')}
    documents={}
    for item in manifest['documents']:
        doc=copy.deepcopy(json.loads((repo_root/'corpus/documents'/item['id']/'document.json').read_text(encoding='utf-8')))
        owned=[x for x in occurrences if x['document_id']==item['id']]
        owners={x['dossier_id'] for x in owned}
        if len(owners)!=1:raise ValueError(f"document source lane ambiguous: {item['id']}")
        classification=classifications[item['id']]
        kind=classification['document_type']
        doc.update(dossier_id=next(iter(owners)), source_path='corpus/'+item['source_path'],
                   occurrences=owned, document_type=kind, title=classification['title'],
                   secondary=kind in SECONDARY_TYPES,
                   appendix_only=kind in SECONDARY_TYPES|PERIPHERAL_TYPES,
                   classification=copy.deepcopy(classification))
        documents[doc['id']]=doc

    raw={}
    provenance={}
    # Corpus IDs stay usable as stable citations. A real cross-namespace collision
    # is refused instead of silently replacing an evidentiary record.
    for path in sorted((repo_root/'corpus/analysis').glob('*.jsonl')):
        for row in _read_jsonl(path):
            if row['id'] in raw:raise ValueError(f"duplicate corpus record ID: {row['id']}")
            raw[row['id']]=row
            provenance[row['id']]={'collection':'corpus-'+path.stem,'path':str(path.relative_to(repo_root))}
    for path in sorted((repo_root/PHASE).glob('*.jsonl')):
        if path.stem in ALIASES or path.stem=='evaluated_calculations':continue
        for row in _read_jsonl(path):
            if row['id'] in raw:raise ValueError(f"conflicting record namespace: {row['id']}")
            raw[row['id']]=row
            provenance[row['id']]={'collection':path.stem,'path':str(path.relative_to(repo_root))}
    # Alias exports are checked and recorded, rather than counted twice.
    for stem in sorted(ALIASES):
        for row in _read_jsonl(repo_root/PHASE/(stem+'.jsonl')):
            if raw.get(row['id'])!=row:raise ValueError(f"noncanonical alias: {stem}/{row['id']}")
            provenance[row['id']].setdefault('aliases',[]).append(str(PHASE/(stem+'.jsonl')))
    evaluations={row['id']:row for row in _read_jsonl(repo_root/PHASE/'evaluated_calculations.jsonl')}
    if set(evaluations)!={key for key in raw if provenance[key]['collection']=='calculations'}:
        raise ValueError('canonical calculation/evaluation join is incomplete')
    ownership={key:_lanes(row,documents) for key,row in raw.items()}
    metadata={key for key,row in raw.items() if row['record_type'] in {'entity','entity_mention','entity_resolution'}}
    records=[]
    lookup={}
    for key in sorted(raw):
        original=raw[key]
        own=ownership[key]
        scoped=key in metadata and len(own)>1
        for lane in sorted(own) if scoped else [next(iter(own)) if len(own)==1 else 'deferred']:
            # Mixed entity objects are indexing projections, not analytical
            # assertions. Copy only neutral label fields: identifiers, flags,
            # attribution and prose may originate exclusively in another lane.
            record=copy.deepcopy({name:original[name] for name in
                                  ('id','record_type','canonical_name','entity_type')
                                  if name in original}) if scoped else copy.deepcopy(original)
            record.update(dossier_id=lane,collection=provenance[key]['collection'],
                          canonical_id=key,canonical_provenance=copy.deepcopy(provenance[key]),
                          dependencies=[],dependency_edges=[],evaluation=copy.deepcopy(evaluations.get(key)),
                          appendix_only=lane=='deferred' or key in metadata or
                            all(documents[CITATION.fullmatch(c)[1]]['appendix_only'] for c in original['source_citations']))
            if scoped:
                record['id']=key+'--'+lane
                record['canonical_record']=copy.deepcopy(original)
                record['source_citations']=[c for c in original['source_citations'] if documents[CITATION.fullmatch(c)[1]]['dossier_id']==lane]
                for field in ('supporting_record_ids','source_mention_ids'):
                    if field in original:
                        record[field]=[dep for dep in original[field] if ownership[dep]<={lane}]
                record['identifiers']={}
                record['evidentiary_status']='indexing_metadata_only'
                record['scope_note']=('Names and types are indexing labels, not cross-source identity joins. '
                                      'Identifiers and mixed-source analytical fields are retained only in audit provenance; '
                                      'consult source-owned supporting records for assertions.')
            record['metadata_references']={name:copy.deepcopy(record[name]) for name in sorted(METADATA_FIELDS) if record.get(name)}
            records.append(record)
            lookup[(key,lane)]=record['id']
    by_id={row['id']:row for row in records}
    for record in records:
        for kind,dependency in _dependency_edges(record):
            if dependency==record['canonical_id']:continue
            if dependency not in raw:raise ValueError(f"missing typed dependency: {record['id']} -> {kind}:{dependency}")
            lane=record['dossier_id']
            target=lookup.get((dependency,lane))
            if not target and lane=='deferred':
                candidates=[row['id'] for row in records if row['canonical_id']==dependency]
                # A deferred statement preserves all evidence edges as audit only.
                for candidate in candidates:record['dependency_edges'].append({'type':kind,'id':candidate})
                continue
            if not target:
                raise ValueError(f"cross-source typed dependency: {record['id']} -> {dependency}")
            record['dependency_edges'].append({'type':kind,'id':target})
        record['dependency_edges']=sorted(record['dependency_edges'],key=lambda edge:(edge['type'],edge['id']))
        record['dependencies']=sorted({edge['id'] for edge in record['dependency_edges']})
    dispositions=[]
    for record in records:
        reason=('Combined statement cites both supplied source lanes; retained for audit only and excluded from dossier findings.'
                if record['dossier_id']=='deferred' else
                'Source-owned entity metadata, restricted to this lane.' if record['canonical_id'] in metadata else
                'Secondary or peripheral source retained in the evidence appendix with original attribution.' if record['appendix_only'] else
                'Included with source-only citations and typed evidence dependencies.')
        dispositions.append({'collection':record['collection'],'id':record['canonical_id'],
                             'record_id':record['id'],'dossier_id':record['dossier_id'],
                             'disposition':'deferred' if record['dossier_id']=='deferred' else 'appendix' if record['appendix_only'] else 'included',
                             'reason':reason})
    counts={lane:{'occurrences':sum(row['dossier_id']==lane for row in occurrences),
                  'documents':sum(row['dossier_id']==lane for row in documents.values()),
                  'records':sum(row['dossier_id']==lane for row in records),
                  **{name:sum(row['dossier_id']==lane and row['collection']==name for row in records) for name in ACCEPTANCE}}
            for lane in (*LANES,'deferred')}
    counts['acceptance']={name:sum(row['collection']==name for row in dispositions) for name in ACCEPTANCE}
    index={'baseline_commit':BASELINE_COMMIT,'dossier_ids':list(LANES),
           'documents':sorted(documents.values(),key=lambda row:row['id']),
           'occurrences':sorted(occurrences,key=lambda row:row['occurrence_id']),
           'records':records,'dispositions':dispositions,'counts':counts}
    return index


def _validate_citation(citation: str, documents: dict, repo_root: Path) -> None:
    match=CITATION.fullmatch(citation)
    if not match or match[1] not in documents:raise ValueError(f'invalid source citation: {citation}')
    doc=documents[match[1]]
    kind,position=match[2],match[3]
    if doc['format']=='pdf':
        if kind!='page' or not position.isdigit() or not 1<=int(position)<=doc['page_count']:
            raise ValueError(f'invalid physical page citation: {citation}')
    elif kind=='page':raise ValueError(f'non-PDF page locator: {citation}')
    elif kind=='section':
        if position!='body':raise ValueError(f'invalid section citation locator: {citation}')
    elif kind in {'line','row'}:
        if not position.isdigit() or int(position)<1:raise ValueError(f'invalid citation locator: {citation}')
        text=(repo_root/doc['source_path']).read_text(encoding='utf-8-sig')
        if kind=='row':
            if doc['format']!='csv':raise ValueError(f'row citation requires CSV: {citation}')
            maximum=len(list(csv.reader(io.StringIO(text))))
        else:
            if doc['format'] not in {'txt','md','paper'}:raise ValueError(f'line citation requires text source: {citation}')
            maximum=len(text.splitlines())
        if int(position)>maximum:raise ValueError(f'citation locator exceeds source: {citation}')


def validate_index(index: dict, repo_root: Path) -> None:
    """Reject unsafe citations, wrong lanes, missing closure and canonical drift."""
    repo_root=Path(repo_root)
    documents={row['id']:row for row in index['documents']}
    records={row['id']:row for row in index['records']}
    if len(records)!=len(index['records']):raise ValueError('duplicate record IDs')
    for row in index['records']:
        if not row.get('source_citations'):raise ValueError(f"missing citation: {row['id']}")
        for citation in row['source_citations']:
            _validate_citation(citation,documents,repo_root)
            lane=documents[CITATION.fullmatch(citation)[1]]['dossier_id']
            if row['dossier_id'] not in {'deferred',lane}:raise ValueError(f"wrong source lane: {row['id']}")
        for dep in row['dependencies']:
            if dep not in records:raise ValueError(f'missing dependency record: {dep}')
            if row['dossier_id']!='deferred' and records[dep]['dossier_id']!=row['dossier_id']:
                raise ValueError(f"wrong dependency lane: {row['id']} -> {dep}")
    expected=build_index(repo_root)
    if index!=expected:raise ValueError('index differs from complete canonical source adapter output')
    if index['counts']['acceptance']!=ACCEPTANCE:raise ValueError('acceptance record count mismatch')
    for lane,occurrences,docs,findings,calculations in [('scout',20,18,17,104),('opeh',21,20,9,25)]:
        counts=index['counts'][lane]
        if [counts[key] for key in ['occurrences','documents','findings','calculations']]!=[occurrences,docs,findings,calculations]:
            raise ValueError(f'financial/source acceptance mismatch: {lane}')
    freeze=repo_root/'dossiers/supplied-files/audit/input-manifest.json'
    if freeze.exists():verify_inputs(repo_root,json.loads(freeze.read_text(encoding='utf-8')))


def main() -> None:
    import argparse
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo-root',type=Path,default=Path(__file__).resolve().parents[3])
    parser.add_argument('--freeze',action='store_true')
    args=parser.parse_args()
    target=args.repo_root/'dossiers/supplied-files'
    freeze=target/'audit/input-manifest.json'
    if args.freeze:
        if freeze.exists():verify_inputs(args.repo_root,json.loads(freeze.read_text(encoding='utf-8')))
        else:freeze_inputs(args.repo_root,freeze)
    index=build_index(args.repo_root)
    validate_index(index,args.repo_root)
    _dump(target/'data/evidence-index.json',index)
    _dump(target/'data/coverage.json',{'baseline_commit':BASELINE_COMMIT,'counts':index['counts'],
                                    'dispositions':index['dispositions']})
    _dump(target/'data/dispositions.json',index['dispositions'])
    print(json.dumps(index['counts'],sort_keys=True))


if __name__=='__main__':main()
