// scripts/analyze-bundle.js
const { execSync } = require('child_process');
const path = require('path');

console.log('🔍 Analyzing bundle size...');

try {
  // Build the project
  execSync('npm run build', { stdio: 'inherit' });
  
  // Install bundle analyzer if not present
  try {
    require.resolve('webpack-bundle-analyzer');
  } catch (e) {
    console.log('📦 Installing webpack-bundle-analyzer...');
    execSync('npm install --save-dev webpack-bundle-analyzer', { stdio: 'inherit' });
  }
  
  // Analyze the bundle
  const buildPath = path.join(__dirname, '../build/static/js');
  execSync(`npx webpack-bundle-analyzer ${buildPath}/*.js`, { stdio: 'inherit' });
  
} catch (error) {
  console.error('❌ Bundle analysis failed:', error.message);
  process.exit(1);
}

