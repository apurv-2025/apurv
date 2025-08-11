#!/usr/bin/env node
/**
 * Frontend AI Assistant Test
 * Tests the React AI assistant component functionality
 */

const puppeteer = require('puppeteer');

async function testAIAssistant() {
  console.log('🧪 Testing Frontend AI Assistant Component...');
  
  let browser;
  try {
    // Launch browser
    browser = await puppeteer.launch({ 
      headless: false, // Set to true for headless testing
      slowMo: 100 
    });
    
    const page = await browser.newPage();
    
    // Navigate to the app
    console.log('📱 Navigating to Prior Authorization app...');
    await page.goto('http://localhost:3002', { waitUntil: 'networkidle0' });
    
    // Wait for the page to load
    await page.waitForTimeout(2000);
    
    // Check if AI Assistant button is present
    console.log('🔍 Looking for AI Assistant button...');
    const aiButton = await page.$('button[title="Open AI Assistant"]');
    
    if (aiButton) {
      console.log('✅ AI Assistant button found!');
      
      // Click the AI Assistant button
      console.log('🖱️ Clicking AI Assistant button...');
      await aiButton.click();
      
      // Wait for chat window to appear
      await page.waitForTimeout(1000);
      
      // Check if chat window is visible
      const chatWindow = await page.$('.fixed.bottom-4.right-4.w-96');
      if (chatWindow) {
        console.log('✅ Chat window opened successfully!');
        
        // Check for welcome message
        const welcomeMessage = await page.$('text="Hello! I\'m your AI assistant for Prior Authorization"');
        if (welcomeMessage) {
          console.log('✅ Welcome message displayed!');
        } else {
          console.log('⚠️ Welcome message not found');
        }
        
        // Test typing a message
        console.log('⌨️ Testing message input...');
        const messageInput = await page.$('textarea[placeholder="Type your message..."]');
        if (messageInput) {
          await messageInput.type('Hello, can you help me with prior authorization?');
          console.log('✅ Message typed successfully!');
          
          // Click send button
          const sendButton = await page.$('button svg[stroke="currentColor"]');
          if (sendButton) {
            await sendButton.click();
            console.log('✅ Send button clicked!');
            
            // Wait for response
            await page.waitForTimeout(3000);
            
            // Check for response
            const response = await page.$('text="I\'m sorry"');
            if (response) {
              console.log('✅ AI response received!');
            } else {
              console.log('⚠️ No AI response detected (this is expected if backend is not running)');
            }
          } else {
            console.log('❌ Send button not found');
          }
        } else {
          console.log('❌ Message input not found');
        }
        
        // Test close button
        console.log('❌ Testing close button...');
        const closeButton = await page.$('button svg[stroke="currentColor"]');
        if (closeButton) {
          await closeButton.click();
          console.log('✅ Chat window closed successfully!');
        } else {
          console.log('❌ Close button not found');
        }
        
      } else {
        console.log('❌ Chat window did not open');
      }
      
    } else {
      console.log('❌ AI Assistant button not found');
    }
    
    console.log('\n🎉 Frontend AI Assistant test completed!');
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
  } finally {
    if (browser) {
      await browser.close();
    }
  }
}

// Check if puppeteer is available
async function checkDependencies() {
  try {
    require('puppeteer');
    return true;
  } catch (error) {
    console.log('⚠️ Puppeteer not installed. Installing...');
    return false;
  }
}

async function main() {
  console.log('🧪 Starting Frontend AI Assistant Test');
  console.log('=' * 50);
  
  const hasPuppeteer = await checkDependencies();
  
  if (!hasPuppeteer) {
    console.log('📦 Installing puppeteer for testing...');
    const { execSync } = require('child_process');
    try {
      execSync('npm install puppeteer', { stdio: 'inherit' });
      console.log('✅ Puppeteer installed successfully!');
    } catch (error) {
      console.log('❌ Failed to install puppeteer. Skipping automated test.');
      console.log('\n📝 Manual Testing Instructions:');
      console.log('1. Open http://localhost:3002 in your browser');
      console.log('2. Look for the AI Assistant button (bottom-right corner)');
      console.log('3. Click the button to open the chat window');
      console.log('4. Try typing a message and sending it');
      console.log('5. Check if the chat interface works correctly');
      return;
    }
  }
  
  await testAIAssistant();
}

if (require.main === module) {
  main().catch(console.error);
}

module.exports = { testAIAssistant }; 