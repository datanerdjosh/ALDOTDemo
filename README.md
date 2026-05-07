# SFBL Life Insurance Agent Assist Portal

An intelligent agent assist portal for life insurance professionals, powered by IBM watsonx Orchestrate AI.

## Overview

The SFBL Agent Assist Portal is designed to support life insurance agents during client consultations by providing instant access to policy information, underwriting guidelines, and compliance requirements through an embedded AI assistant.

## Features

- **Professional Agent Interface**: Clean, intuitive design optimized for agent workflows
- **Quick Access Tools**: Fast navigation to client profiles, policy guidelines, and underwriting tools
- **AI-Powered Agent Assist**: Real-time support during client consultations via IBM watsonx Orchestrate
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile devices
- **Secure Authentication**: Protected access for authorized agents only

## IBM watsonx Orchestrate Integration

The portal includes an embedded AI assistant that provides real-time support to agents during client consultations. The assistant can help with:

- **Policy Coverage Details**: Instant access to coverage options, exclusions, and policy terms
- **Underwriting Guidelines**: Risk assessment criteria, approval requirements, and medical underwriting rules
- **Premium Calculations**: Quote generation, discount eligibility, and rate factors
- **Compliance Questions**: Regulatory requirements, disclosure obligations, and documentation needs
- **Product Comparisons**: Side-by-side analysis of different policy options and recommendations

### Configuration

The chat widget is configured with the following parameters:

- **Orchestration ID**: `93786cf852c24f1996c852ed6dbb3de4_73a624f5-40ec-4066-aec9-164dff7ad428`
- **Host URL**: `https://us-south.watson-orchestrate.cloud.ibm.com`
- **Agent ID**: `208884f7-e996-4769-9b24-0af61a7dba68`
- **Agent Environment ID**: `2d0911b2-8ea1-4650-8f74-a736763484ef`

## Files

- `index.html` - Main portal interface with embedded AI assistant
- `login.html` - Secure agent authentication page
- `styles.css` - Professional styling for the agent portal
- `login-styles.css` - Login page styling
- `auth.js` - Authentication logic
- `README.md` - This documentation file

## Running the Application

### Option 1: Python HTTP Server

```bash
cd ALDOTDemo
python3 -m http.server 8080
```

Then open your browser to `http://localhost:8080`

### Option 2: Node.js HTTP Server

```bash
cd SFBLDemo
npx http-server -p 8000
```

Then open your browser to `http://localhost:8000`

### Option 3: VS Code Live Server

1. Install the "Live Server" extension in VS Code
2. Right-click on `index.html`
3. Select "Open with Live Server"

## Authentication

The portal uses session-based authentication. Demo credentials are provided on the login page for testing purposes.

**Note**: In production, implement proper authentication with your organization's identity provider.

## Use Cases

### During Client Consultations

Agents can use the AI assistant to:
- Quickly verify policy details while on the phone with clients
- Check underwriting requirements for specific health conditions
- Calculate premium estimates with various coverage options
- Confirm compliance requirements for specific situations
- Compare product features to recommend the best fit

### Pre-Meeting Preparation

- Review client history and existing policies
- Research product options for upcoming consultations
- Verify current guidelines and requirements
- Access training materials and best practices

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

All styles are contained in `styles.css` and `login-styles.css`. Key color scheme:

- **Primary Blue**: `#0d4f8b` to `#1a6fb0` (gradient)
- **Background**: `#f8f9fa`
- **Footer**: `#1a3a52`
- **Text**: `#333`

The color palette is designed to convey trust, professionalism, and stability - key attributes for life insurance services.

## Browser Compatibility

- Chrome (recommended)
- Firefox
- Safari
- Edge

## Security Notes

- This is a demonstration application
- In production, implement proper authentication and authorization
- Use HTTPS for all connections
- Follow your organization's security and compliance policies
- Ensure all client data is handled according to privacy regulations (HIPAA, etc.)

## Support

For technical issues with the IBM watsonx Orchestrate integration, refer to the [IBM watsonx Orchestrate documentation](https://www.ibm.com/docs/en/watsonx/watson-orchestrate).

For agent support or training questions, contact your SFBL Agent Support Services team.

## License

This is a demonstration project for internal use by SFBL life insurance agents.

---

**Made with Bob** - AI-Powered Development Assistant