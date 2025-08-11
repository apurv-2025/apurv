#!/usr/bin/env node
/*
Quick test to verify the navigation structure for InsuranceVerification
*/

const fs = require('fs');
const path = require('path');

console.log('🧪 Testing InsuranceVerification Navigation Structure');
console.log('=' .repeat(50));

// Check if AgentPage exists
const agentPagePath = path.join(__dirname, 'frontend/src/pages/AgentPage.js');
if (fs.existsSync(agentPagePath)) {
    console.log('✅ AgentPage.js exists');
} else {
    console.log('❌ AgentPage.js missing');
}

// Check if agent components exist
const agentComponents = [
    'frontend/src/components/agent/AgentChat.js',
    'frontend/src/components/agent/AgentTools.js',
    'frontend/src/components/agent/AgentDashboard.js'
];

agentComponents.forEach(component => {
    const componentPath = path.join(__dirname, component);
    if (fs.existsSync(componentPath)) {
        console.log(`✅ ${component} exists`);
    } else {
        console.log(`❌ ${component} missing`);
    }
});

// Check App.js for AgentPage import
const appJsPath = path.join(__dirname, 'frontend/src/App.js');
if (fs.existsSync(appJsPath)) {
    const appJsContent = fs.readFileSync(appJsPath, 'utf8');
    if (appJsContent.includes('import AgentPage')) {
        console.log('✅ AgentPage import found in App.js');
    } else {
        console.log('❌ AgentPage import missing in App.js');
    }
    
    if (appJsContent.includes('/agent')) {
        console.log('✅ /agent route found in App.js');
    } else {
        console.log('❌ /agent route missing in App.js');
    }
} else {
    console.log('❌ App.js missing');
}

// Check Navigation.js for AI Assistant tab
const navigationPath = path.join(__dirname, 'frontend/src/components/layout/Navigation.js');
if (fs.existsSync(navigationPath)) {
    const navigationContent = fs.readFileSync(navigationPath, 'utf8');
    if (navigationContent.includes('AI Assistant')) {
        console.log('✅ AI Assistant tab found in Navigation.js');
    } else {
        console.log('❌ AI Assistant tab missing in Navigation.js');
    }
    
    if (navigationContent.includes('Bot')) {
        console.log('✅ Bot icon import found in Navigation.js');
    } else {
        console.log('❌ Bot icon import missing in Navigation.js');
    }
} else {
    console.log('❌ Navigation.js missing');
}

console.log('\n🎯 Navigation Structure Test Complete!');
console.log('The AI Assistant tab should now appear next to Dashboard in the navigation.'); 