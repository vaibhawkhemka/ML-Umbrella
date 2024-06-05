const puppeteer = require('puppeteer-extra');
const StealthPlugin = require('puppeteer-extra-plugin-stealth');
puppeteer.use(StealthPlugin());

const url = process.argv[2];
//const url = "https://www.linkedin.com/posts/aboniasojasingarayar_llm-agent-toolkit-activity-7198223445225000960-Z9zc/"
const timeout = 10000;

(async () => {
    const browser = await puppeteer.launch( {
        headless: "new",
    } );

    const page = await browser.newPage();

    await page.setViewport( {
        width: 1200,
        height: 1200,
        deviceScaleFactor: 1,
    } );

    setTimeout(async () => {
        await page.screenshot( {
            path: "screenshot.jpg",
            fullPage: true,
        } );
    }, timeout-2000);

    await page.goto( url, {
        waitUntil: "networkidle0",
        timeout: timeout,
    } );

    await page.screenshot( {
        path: "screenshot.jpg",
        fullPage: true,
    } );

    await browser.close();
})();