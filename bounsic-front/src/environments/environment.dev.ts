export const environment = {
    production: false,
    // apiUrl: 'http://localhost:1801', //back
    // api_S_Url: 'http://localhost:4000', //stream

    apiUrl: 'https://bounsic.site', //back // http://20.81.217.99:1801
    api_S_Url: 'https://streaming-cchyanf7gdhch9az.eastus2-01.azurewebsites.net', //streaming // https://streaming-cchyanf7gdhch9az.eastus2-01.azurewebsites.net

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