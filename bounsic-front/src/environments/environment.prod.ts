export const environment = {
    production: true,
    apiUrl: 'http://bounsic-back-nginx-gbh0hce0c7ada6gk.eastus2-01.azurewebsites.net', //back
    msalConfig: {
        auth: {
            clientId: '358ef62a-08c7-4755-9a61-78f1ebd0cd49',
            authority: 'https://login.microsoftonline.com/618bab0f-20a4-4de3-a10c-e20cee96bb35'
        }
    },
    apiConfig: {
        scopes: ['user.read'],
        uri: 'https://graph.microsoft.com/v1.0/me'
    }
};