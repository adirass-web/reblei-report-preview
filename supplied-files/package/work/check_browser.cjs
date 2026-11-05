/* Offline and HTTP browser checks; output is a reproducible review summary. */
const {chromium} = require('playwright');
const {pathToFileURL} = require('url');
const path = require('path');
const http = require('http');
const fs = require('fs');
const root = path.resolve(process.argv[2] || path.join(__dirname, '../presentation'));
const check = (ok, message) => {if (!ok) throw Error(message)};
(async () => {
  fs.mkdirSync(path.join(root, 'review'), {recursive:true});
  const executablePath = process.env.CHROMIUM_PATH || (fs.existsSync('/usr/bin/chromium') ? '/usr/bin/chromium' : undefined);
  const browser = await chromium.launch({headless:true, executablePath, args:['--no-sandbox']});
  const results = [];
  const server = http.createServer((req,res) => {
    const file = path.resolve(root, '.' + decodeURIComponent(new URL(req.url,'http://localhost').pathname));
    if (!(file === root || file.startsWith(root + path.sep))) {res.writeHead(403); return res.end()}
    fs.readFile(file, (err,data) => {if(err){res.writeHead(404);return res.end()} const ext=path.extname(file); res.setHeader('Content-Type',({'.html':'text/html; charset=utf-8','.css':'text/css','.js':'application/javascript','.png':'image/png','.pdf':'application/pdf'})[ext] || 'application/octet-stream'); res.end(data)});
  });
  await new Promise(resolve => server.listen(0,'127.0.0.1',resolve));
  try {
    for (const mode of ['file','http']) {
      const context = await browser.newContext({viewport:{width:1280,height:900}});
      await context.route('**/*', route => {const u=new URL(route.request().url()); if (u.protocol === 'file:' || (u.hostname === '127.0.0.1' && Number(u.port) === server.address().port)) route.continue(); else route.abort()});
      const page = await context.newPage();
      const url = mode === 'file' ? pathToFileURL(path.join(root,'scout/records.html')).href : `http://127.0.0.1:${server.address().port}/scout/records.html`;
      try { await page.goto(url); } catch (e) {
        if (mode === 'file' && String(e).includes('ERR_BLOCKED_BY_ADMINISTRATOR')) {results.push('file: BLOCKED by managed Chromium URL policy'); await context.close(); continue;}
        throw e;
      }
      const n=await page.locator('.record').count(); check(n>0, `${mode}: no records`);
      const id=await page.locator('.record').first().getAttribute('id');
      await page.locator('#search').fill(id); await page.waitForTimeout(250);
      check(await page.locator('.record:visible').count() >= 1, `${mode}: search failed`);
      await page.locator('#search').fill('zzzz-no-such-record-zzzz'); await page.waitForTimeout(250);
      check(await page.locator('.record:visible').count() === 0, `${mode}: filter failed`);
      await page.emulateMedia({media:'print'}); check(await page.locator('.record:visible').count() === n, `${mode}: print hides filtered records`);
      await page.emulateMedia({media:'screen'}); await page.locator('#reset').click();
      await page.locator('#filter-collection').focus();
      check(await page.locator('#filter-collection').evaluate(el => document.activeElement === el), `${mode}: collection filter did not receive focus`);
      await page.keyboard.press('Tab');
      check(await page.locator('#reset').evaluate(el => document.activeElement === el), `${mode}: Tab did not move focus to Clear filters`);
      await page.setViewportSize({width:375,height:812}); check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), `${mode}: mobile overflow`);
      await page.goto(mode === 'file' ? pathToFileURL(path.join(root,'scout/sources.html')).href : `http://127.0.0.1:${server.address().port}/scout/sources.html`);
      check(await page.locator('a[download]').count()>0, `${mode}: no original links`);
      results.push(`${mode}: search, filters, print visibility, keyboard, mobile and evidence links passed`);
      await context.close();
    }
    const context=await browser.newContext({javaScriptEnabled:false}); const page=await context.newPage();
    await page.goto(`http://127.0.0.1:${server.address().port}/opeh/records.html`);
    check(await page.locator('.record:visible').count()>0,'no-JS records unavailable');
    results.push('HTTP, JavaScript disabled: records visible');
    for (const lane of ['scout','opeh']) {
      await page.goto(`http://127.0.0.1:${server.address().port}/${lane}/index.html`);
      await page.screenshot({path:path.join(root,'review',lane+'-desktop.png')});
      await page.setViewportSize({width:375,height:812});
      check(await page.evaluate(() => document.documentElement.scrollWidth <= innerWidth + 1), lane + ': report mobile overflow');
      await page.screenshot({path:path.join(root,'review',lane+'-mobile.png')});
      await page.setViewportSize({width:1280,height:900});
      try { await page.pdf({path:path.join(root,'review',lane+'-report.pdf'),format:'A4',printBackground:true,timeout:30000}); results.push(lane + ' report A4 PDF generated'); } catch(e) { results.push(lane + ' report PDF unavailable: ' + e.message); }
    } await context.close();
    fs.writeFileSync(path.join(root,'review','browser-check.txt'),results.join('\n')+'\n'); console.log(results.join('\n'));
  } finally {server.close(); await browser.close()}
})().catch(e => {console.error(e); process.exitCode=1});
