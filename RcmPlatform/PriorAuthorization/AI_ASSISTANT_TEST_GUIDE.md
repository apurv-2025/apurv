# AI Assistant Test Guide

## Quick Test Instructions

### 1. Start the System

```bash
cd RcmPlatform/PriorAuthorization
./start_integrated.sh
```

### 2. Verify Services are Running

Check that all services are running:
- Patient Microservice: http://localhost:8000
- Prior Authorization API: http://localhost:8002
- Prior Authorization Frontend: http://localhost:3002

### 3. Test AI Assistant Frontend

#### Option A: Dedicated AI Assistant Tab
1. **Open the application**: Navigate to http://localhost:3002
2. **Click "AI Assistant" tab**: Located in the navigation menu (second tab after Dashboard)
3. **Check the dedicated page**: Should show a full AI Assistant interface with:
   - Header with AI Assistant title and status
   - Large chat interface on the left
   - Sidebar with examples, tools, and quick actions on the right
4. **Try typing a message**: Type "Hello" and press Enter
5. **Check response**: Should receive a response (may be fallback if backend not fully configured)

#### Option B: Floating Chat Widget
1. **Open the application**: Navigate to http://localhost:3002
2. **Look for AI Assistant button**: Bottom-right corner of the screen (blue circular button)
3. **Click the button**: Should open a floating chat window
4. **Check welcome message**: Should see "Hello! I'm your AI assistant for Prior Authorization"
5. **Try typing a message**: Type "Hello" and press Enter
6. **Check response**: Should receive a response (may be fallback if backend not fully configured)

### 4. Test AI Assistant API

```bash
# Test AI health
curl http://localhost:8002/api/v1/agent/health

# Test chat functionality
curl -X POST http://localhost:8002/api/v1/agent/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "user_id": "test_user"}'

# Test available tools
curl http://localhost:8002/api/v1/agent/tools

# Test examples
curl http://localhost:8002/api/v1/agent/examples
```

### 5. Test AI Tools

```bash
# Test prior authorization creation
curl -X POST http://localhost:8002/api/v1/agent/create-prior-auth \
  -H "Content-Type: application/json" \
  -d '{
    "patient_id": "PAT123456",
    "provider_npi": "1234567890",
    "procedure_codes": [{"code": "99213", "description": "Office visit"}],
    "diagnosis_codes": [{"code": "E11.9", "description": "Diabetes"}]
  }'

# Test EDI generation
curl -X POST http://localhost:8002/api/v1/agent/generate-edi \
  -H "Content-Type: application/json" \
  -d '{
    "edi_type": "278",
    "patient_id": "PAT123456",
    "provider_npi": "1234567890"
  }'

# Test code lookup
curl -X POST http://localhost:8002/api/v1/agent/lookup-codes \
  -H "Content-Type: application/json" \
  -d '{
    "code_type": "procedure",
    "search_term": "office visit"
  }'
```

## Expected Results

### Frontend Tests - Dedicated Tab
- ✅ AI Assistant tab visible in navigation menu (second position)
- ✅ Tab has Bot icon and proper styling
- ✅ Dedicated page loads with full AI Assistant interface
- ✅ Header shows AI Assistant title and status indicator
- ✅ Large chat interface is functional
- ✅ Sidebar shows examples, tools, and quick actions
- ✅ Message input field works
- ✅ Send button is functional
- ✅ Clear chat button works

### Frontend Tests - Floating Widget
- ✅ AI Assistant button visible in bottom-right corner
- ✅ Chat window opens when button clicked
- ✅ Welcome message displayed
- ✅ Message input field functional
- ✅ Send button works
- ✅ Chat window closes properly

### API Tests
- ✅ Health check returns status
- ✅ Chat endpoint responds
- ✅ Tools endpoint returns available tools
- ✅ Examples endpoint returns sample interactions
- ✅ Tool endpoints execute successfully

### Navigation Tests
- ✅ AI Assistant tab appears in navigation menu
- ✅ Tab is positioned correctly (second after Dashboard)
- ✅ Tab has proper active/inactive styling
- ✅ Clicking tab navigates to AI Assistant page
- ✅ Tab icon (Bot) displays correctly

### Common Issues and Solutions

#### 1. "Cannot find module 'axios'" Error
**Solution**: The axios dependency has been added to package.json. Run:
```bash
cd frontend
npm install
```

#### 2. Tailwind CSS Classes Not Working
**Solution**: Tailwind CSS is configured. If styles aren't working, restart the frontend:
```bash
cd frontend
npm start
```

#### 3. AI Assistant Tab Not Visible
**Solution**: Check that the Navigation component has been updated and the route is added to App.js

#### 4. AI Assistant Not Responding
**Solution**: This is expected if agentic-core is not fully configured. The system includes fallback responses.

#### 5. Backend API Errors
**Solution**: Check that the backend is running and the database is accessible.

## Manual Verification Checklist

### Navigation Interface
- [ ] AI Assistant tab appears in navigation menu
- [ ] Tab is positioned second after Dashboard
- [ ] Tab has Bot icon
- [ ] Tab has proper active/inactive styling
- [ ] Clicking tab navigates to AI Assistant page
- [ ] URL changes to /ai-assistant when tab is clicked

### Dedicated AI Assistant Page
- [ ] Page loads with proper layout
- [ ] Header shows AI Assistant title and status
- [ ] Large chat interface is present on the left
- [ ] Sidebar is present on the right
- [ ] Examples section shows sample interactions
- [ ] Tools section shows available AI tools
- [ ] Quick Actions section shows common tasks
- [ ] Chat interface is fully functional
- [ ] Message input and send button work
- [ ] Clear chat button works

### Floating Widget (Still Available)
- [ ] AI Assistant button appears in bottom-right corner
- [ ] Button has proper hover effects
- [ ] Chat window opens smoothly
- [ ] Welcome message is displayed
- [ ] Message input field is functional
- [ ] Send button is clickable
- [ ] Chat window can be closed
- [ ] Messages display with proper styling
- [ ] Loading indicators work
- [ ] Example suggestions appear (if available)

### API Functionality
- [ ] Health check endpoint responds
- [ ] Chat endpoint accepts messages
- [ ] Tools endpoint returns tool list
- [ ] Examples endpoint returns examples
- [ ] Tool execution endpoints work
- [ ] Error handling works properly
- [ ] Response format is correct

### Integration
- [ ] Frontend can communicate with backend
- [ ] AI assistant integrates with existing Prior Authorization system
- [ ] Patient microservice integration works
- [ ] EDI generation works
- [ ] Code lookup functionality works
- [ ] Both dedicated page and floating widget work independently

## Troubleshooting

### Frontend Issues
1. **Module not found errors**: Run `npm install` in the frontend directory
2. **Styling issues**: Ensure Tailwind CSS is properly configured
3. **Component not loading**: Check for JavaScript errors in browser console
4. **Tab not appearing**: Verify Navigation.js has been updated with AI Assistant tab

### Backend Issues
1. **API not responding**: Check if backend service is running
2. **Database errors**: Verify database connection and schema
3. **Import errors**: Check Python dependencies and imports

### Integration Issues
1. **CORS errors**: Ensure proper CORS configuration
2. **Network errors**: Check service URLs and ports
3. **Authentication issues**: Verify API key configuration

## Success Criteria

The AI assistant integration is successful when:

1. ✅ Frontend loads without errors
2. ✅ AI Assistant tab is visible in navigation menu
3. ✅ Dedicated AI Assistant page loads and functions properly
4. ✅ Floating chat widget still works as before
5. ✅ Chat interface opens and responds to user input
6. ✅ API endpoints return proper responses
7. ✅ AI tools execute successfully
8. ✅ Integration with existing Prior Authorization system works
9. ✅ Error handling works gracefully
10. ✅ Fallback mechanisms function when AI services unavailable

## Next Steps

After successful testing:

1. **Configure AI Model**: Set up proper AI model provider and API keys
2. **Customize Tools**: Adapt AI tools for specific business requirements
3. **Add Authentication**: Implement user authentication for conversation history
4. **Performance Optimization**: Add caching and rate limiting
5. **Monitoring**: Set up logging and monitoring for AI assistant usage
6. **User Training**: Create user guides for the new AI Assistant tab 