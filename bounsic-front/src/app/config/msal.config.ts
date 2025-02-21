import { IPublicClientApplication, PublicClientApplication, InteractionType, BrowserCacheLocation, LogLevel } from '@azure/msal-browser';
import { environment } from 'src/environments/environment.dev';
import { MsalInterceptorConfiguration, MsalGuardConfiguration } from '@azure/msal-angular';

export function loggerCallback(logLevel: LogLevel, message: string) {
    console.log(message);
}

export function MSALInstanceFactory(): IPublicClientApplication {
    return new PublicClientApplication({
        auth: {
            clientId: environment.msalConfig.auth.clientId,
            authority: environment.msalConfig.auth.authority,
            redirectUri: 'http://localhost:4200/dashboard',
            postLogoutRedirectUri: '/'
        },
        cache: {
            cacheLocation: BrowserCacheLocation.LocalStorage
        },
        system: {
            // allowNativeBroker: false, // Disables WAM Broker
            loggerOptions: {
                loggerCallback,
                logLevel: LogLevel.Info,
                piiLoggingEnabled: false
            }
        }
    });
}

export function MSALInterceptorConfigFactory(): MsalInterceptorConfiguration {
    const protectedResourceMap = new Map<string, Array<string>>();
    protectedResourceMap.set(environment.apiConfig.uri, environment.apiConfig.scopes);

    return {
        interactionType: InteractionType.Redirect,
        protectedResourceMap
    };
}

export function MSALGuardConfigFactory(): MsalGuardConfiguration {
    return {
        interactionType: InteractionType.Redirect,
        authRequest: {
            scopes: [...environment.apiConfig.scopes]
        },
        loginFailedRoute: '/login-failed'
    };
}