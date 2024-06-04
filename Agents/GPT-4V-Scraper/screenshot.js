// const puppeteer = require('puppeteer-extra');
// const StealthPlugin = require('puppeteer-extra-plugin-stealth');
// puppeteer.use(StealthPlugin());

// // const url = process.argv[2];
// const url = "https://en.wikipedia.org/wiki/India"
// const timeout = 5000;

// (async () => {
//     const browser = await puppeteer.launch( {
//         headless: "false",
//         // executablePath: '/Applications/Google\ Chrome\ Canary.app/Contents/MacOS/Google\ Chrome\ Canary',
//         // userDataDir: '/Users/jasonzhou/Library/Application\ Support/Google/Chrome\ Canary/Default',
//     } );

//     const page = await browser.newPage();

//     await page.setViewport( {
//         width: 1200,
//         height: 1200,
//         deviceScaleFactor: 1,
//     } );

//     await page.goto( url, {
//         waitUntil: "domcontentloaded",
//         timeout: timeout,
//     } );

//     await page.waitForTimeout(timeout);

//     await page.screenshot({
//         path: "screenshot.jpg",
//         fullPage: true,
//     });

//     await browser.close();
// })();