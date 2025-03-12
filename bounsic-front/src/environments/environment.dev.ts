export const environment = {
    production: false,
    apiUrl: 'http://localhost:1801', //back
    msalConfig: {
        auth: {
            clientId: '69070e99-af46-49f0-a4f4-228ac2f8b61f',
            authority: 'https://login.microsoftonline.com/af2aa024-2160-4e82-a754-865b614d0ff9'
        }
    },
    apiConfig: {
        scopes: ['user.read'],
        uri: 'https://graph.microsoft.com/v1.0/me'
    }
};