import { Injectable, Inject, PLATFORM_ID, OnDestroy } from '@angular/core';
import { Router } from '@angular/router';
import { isPlatformBrowser } from '@angular/common';
import { Subject, filter, takeUntil } from 'rxjs';
import {
  MsalService,
  MsalBroadcastService
} from '@azure/msal-angular';
import {
  EventMessage,
  EventType,
  InteractionStatus,
  PopupRequest,
  RedirectRequest
} from '@azure/msal-browser';

@Injectable({
  providedIn: 'root',
})
export class AuthService implements OnDestroy {
  private readonly _destroying$ = new Subject<void>();
  isIframe = false;
  loginDisplay = false;
  userProfile: any = null;

  constructor(
    private msalService: MsalService,
    private msalBroadcastService: MsalBroadcastService,
    private router: Router,
    @Inject(PLATFORM_ID) private platformId: object
  ) {}

  initialize(): void {
    if (isPlatformBrowser(this.platformId)) {
      // Manejar loginRedirect
      this.msalService.handleRedirectObservable()
        .pipe(takeUntil(this._destroying$))
        .subscribe({
          next: (result) => {
            if (result && result.account) {
              this.msalService.instance.setActiveAccount(result.account);
              this.setLoginDisplay();
            }
          },
          error: (error) => {
            console.error('Redirect error:', error);
          }
        });

      this.isIframe = window !== window.parent && !window.opener;
    }

    this.msalService.instance.enableAccountStorageEvents();

    // Actualiza cuando se agregan o eliminan cuentas
    this.msalBroadcastService.msalSubject$
      .pipe(
        filter((msg: EventMessage) =>
          msg.eventType === EventType.ACCOUNT_ADDED ||
          msg.eventType === EventType.ACCOUNT_REMOVED
        ),
        takeUntil(this._destroying$)
      )
      .subscribe(() => {
        if (this.msalService.instance.getAllAccounts().length === 0) {
          this.router.navigate(['/']);
        } else {
          this.checkAndSetActiveAccount();
          this.setLoginDisplay();
        }
      });

    // Detecta cuando ya no hay interacción para actualizar el estado
    this.msalBroadcastService.inProgress$
      .pipe(
        filter((status: InteractionStatus) => status === InteractionStatus.None),
        takeUntil(this._destroying$)
      )
      .subscribe(() => {
        this.checkAndSetActiveAccount();
        this.setLoginDisplay();
      });
  }

  /**
   * Iniciar sesión con popup (alternativa al redirect)
   */
  loginPopup(authRequest?: PopupRequest) {
    return this.msalService.loginPopup(authRequest)
      .pipe(takeUntil(this._destroying$))
      .toPromise()
      .then((response) => {
        if (response && response.account) {
          this.msalService.instance.setActiveAccount(response.account);
          this.setLoginDisplay();
        }
        return response;
      });
  }

  /**
   * Iniciar sesión con redirect
   */
  loginRedirect(authRequest?: RedirectRequest) {
    return this.msalService.loginRedirect(authRequest);
  }

  /**
   * Cerrar sesión
   */
  logout(popup = false): void {
    if (popup) {
      this.msalService.logoutPopup({ mainWindowRedirectUri: '/' });
    } else {
      this.msalService.logoutRedirect();
    }
    this.msalService.instance.logout();
    localStorage.clear(); 
    sessionStorage.clear();
    document.cookie = 'msalAppState=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
    document.cookie = 'msal.msalConfig=; expires=Thu, 01 Jan 1970 00:00:00 GMT; path=/';
    this.userProfile = null;
  }

  /**
   * Verifica cuentas activas y actualiza la sesión
   */
  private setLoginDisplay(): void {
    const accounts = this.msalService.instance.getAllAccounts();
    this.loginDisplay = accounts.length > 0;

    if (this.loginDisplay) {
      const activeAccount = this.msalService.instance.getActiveAccount();
      this.userProfile = activeAccount;
    }
  }

  /**
   * Si no hay cuenta activa, elige la primera disponible
   */
  private checkAndSetActiveAccount(): void {
    let activeAccount = this.msalService.instance.getActiveAccount();
    if (!activeAccount) {
      const accounts = this.msalService.instance.getAllAccounts();
      if (accounts.length > 0) {
        this.msalService.instance.setActiveAccount(accounts[0]);
      }
    }
  }

  /**
   * Obtener el perfil del usuario autenticado
   */
  getUserProfile(): any {
    return this.userProfile;
  }

  /**
   * Limpia el observable al destruir el servicio
   */
  ngOnDestroy(): void {
    this._destroying$.next();
    this._destroying$.complete();
  }
}
