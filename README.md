# Bank Employee Portal with IBM watsonx Orchestrate

A professional banking employee portal website with an embedded IBM watsonx Orchestrate AI assistant.

## Features

- **Clean, Professional Design**: Modern banking interface with intuitive navigation
- **Quick Action Cards**: Easy access to common banking tasks
- **Embedded AI Assistant**: IBM watsonx Orchestrate chat widget for employee support
- **Responsive Layout**: Works on desktop, tablet, and mobile devices

## IBM watsonx Orchestrate Integration

The portal includes an embedded AI assistant powered by IBM watsonx Orchestrate that can help employees with:

- Customer account inquiries
- Policy and procedure questions
- System navigation assistance
- Report generation guidance

### Configuration

The chat widget is configured with the following parameters:

- **Orchestration ID**: `1d334f6f5c4a402389b1001f50d6565d_47c38f8e-44f5-4baf-a53e-3034947b68eb`
- **Host URL**: `https://us-south.watson-orchestrate.cloud.ibm.com`
- **Agent ID**: `9f708ab0-4b49-4d2e-bfbb-eb3b4a79520a`
- **Agent Environment ID**: `9aaf2025-519f-47b4-b2a9-1fd4fb14f477`

## Files

- `index.html` - Main HTML structure with embedded chat widget
- `styles.css` - Professional styling for the banking portal
- `README.md` - This documentation file

## Running the Application

### Option 1: Python HTTP Server

```bash
cd HWBDemo
python3 -m http.server 8000
```

Then open your browser to `http://localhost:8000`

### Option 2: Node.js HTTP Server

```bash
cd HWBDemo
npx http-server -p 8000
```

Then open your browser to `http://localhost:8000`

### Option 3: VS Code Live Server

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## Customization

### Updating the Chat Widget

To update the IBM watsonx Orchestrate configuration, modify the `window.wxOConfiguration` object in `index.html`:

```javascript
window.wxOConfiguration = {
    orchestrationID: "your-orchestration-id",
    hostURL: "your-host-url",
    rootElementID: "root",
    deploymentPlatform: "ibmcloud",
    crn: "your-crn",
    chatOptions: {
        agentId: "your-agent-id", 
        agentEnvironmentId: "your-environment-id",
    }
};
```

### Styling

All styles are contained in `styles.css`. Key color variables:

- Primary Blue: `#1e3c72` to `#2a5298` (gradient)
- Purple Gradient: `#667eea` to `#764ba2`
- Background: `#f5f7fa`
- Footer: `#2c3e50`

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Security Notes

- This is a demo application
- In production, implement proper authentication
- Use HTTPS for all connections
- Follow your organization's security policies

## Support

For technical issues with the IBM watsonx Orchestrate integration, refer to the [IBM watsonx Orchestrate documentation](https://www.ibm.com/docs/en/watsonx/watson-orchestrate).

## License

This is a demonstration project for internal use.