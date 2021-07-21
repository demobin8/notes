var args = process.argv.splice(2);
var url = args[0];
var output_path = args[1];

const puppeteer = require('puppeteer');

(async () => {
  try {
    const browser = await puppeteer.launch({args: ['--no-sandbox']});
    const page = await browser.newPage();
    const rsp = await page.goto(url);
	
    await page.pdf({path: output_path, format: 'A4', displayHeaderFooter: false, margin: {top: 20, left: 25, bottom: 20}, scale: 1});

    await browser.close();
  } catch(err) {
    console.error(err);
  }
})();

