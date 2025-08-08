// Performance monitoring script
// scripts/performance-check.js
const lighthouse = require('lighthouse');
const chromeLauncher = require('chrome-launcher');

async function runLighthouse() {
  const chrome = await chromeLauncher.launch({ chromeFlags: ['--headless'] });
  const options = { logLevel: 'info', output: 'html', onlyCategories: ['performance'] };
  const runnerResult = await lighthouse('http://localhost:3000', options);
  
  // Output the result
  console.log('Performance score:', runnerResult.lhr.categories.performance.score * 100);
  
  await chrome.kill();
}

if (require.main === module) {
  runLighthouse().catch(console.error);
}

module.exports = { runLighthouse };
