const fs = require('fs');
const path = require('path');

const imageDir = path.join(__dirname, '../public');
const targetSize = 1024 * 1024; // 1MB

function checkImageSizes(dir) {
  const files = fs.readdirSync(dir);
  
  files.forEach(file => {
    const filePath = path.join(dir, file);
    const stats = fs.statSync(filePath);
    
    if (stats.isFile() && /\.(jpg|jpeg|png|gif|svg)$/i.test(file)) {
      if (stats.size > targetSize) {
        console.log(`⚠️  Large image detected: ${file} (${(stats.size / 1024 / 1024).toFixed(2)}MB)`);
        console.log(`   Consider optimizing this image for better performance.`);
      }
    }
  });
}

console.log('🖼️  Checking image sizes...');
checkImageSizes(imageDir);
console.log('✅ Image size check complete!');
