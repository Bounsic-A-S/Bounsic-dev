import { ChangeDetectionStrategy, Component, Inject, OnDestroy, OnInit, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { filter, Subject, takeUntil } from 'rxjs';
import { MSAL_GUARD_CONFIG, MsalBroadcastService, MsalGuardConfiguration, MsalService } from '@azure/msal-angular';
import { AuthenticationResult, EventMessage, EventType, InteractionStatus, PopupRequest, RedirectRequest } from '@azure/msal-browser';
import { Router, RouterModule } from '@angular/router';


@Component({
  selector: 'main-navbar',
  templateUrl: './navbar-app.component.html',
  standalone: true,
  imports: [CommonModule,RouterModule],
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class NavbarAppComponent implements OnInit, OnDestroy {
  isMobileMenuOpen = false;
  userProfile: any = null;
  isLoggingToggled = false;
  isIframe = false;
  loginDisplay = false;
  private readonly _destroying$ = new Subject<void>();

  constructor(
    @Inject(PLATFORM_ID) private platformId: object,
    @Inject(MSAL_GUARD_CONFIG) private msalGuardConfig: MsalGuardConfiguration,
    private authService: MsalService,
    private msalBroadcastService: MsalBroadcastService,
    private router: Router
  ) { }

  ngOnInit(): void {
    if (isPlatformBrowser(this.platformId)) {
      this.authService.handleRedirectObservable().subscribe();
      this.isIframe = window !== window.parent && !window.opener;
    }

    this.authService.instance.enableAccountStorageEvents();

    // Manejar eventos de cuenta
    this.msalBroadcastService.msalSubject$
      .pipe(
        filter((msg: EventMessage) => msg.eventType === EventType.ACCOUNT_ADDED || msg.eventType === EventType.ACCOUNT_REMOVED),
        takeUntil(this._destroying$)
      )
      .subscribe(() => {
        if (this.authService.instance.getAllAccounts().length === 0) {
          this.router.navigate(['/']);
        } else {
          this.checkAndSetActiveAccount(); // Asegurar cuenta activa antes de mostrar el perfil
          this.setLoginDisplay();
        }
      });

    // Manejar eventos de estado de autenticación
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

  private setLoginDisplay(): void {
    const accounts = this.authService.instance.getAllAccounts();
    this.loginDisplay = accounts.length > 0;

    if (this.loginDisplay) {
      const activeAccount = this.authService.instance.getActiveAccount();
      this.userProfile = activeAccount ? activeAccount : null;
    }
  }

  private checkAndSetActiveAccount(): void {
    let activeAccount = this.authService.instance.getActiveAccount();
    if (!activeAccount) {
      const accounts = this.authService.instance.getAllAccounts();
      if (accounts.length > 0) {
        this.authService.instance.setActiveAccount(accounts[0]);
      }
    }
  }

  loginRedirect(): void {
    if (this.msalGuardConfig.authRequest) {
      this.authService.loginRedirect({ ...this.msalGuardConfig.authRequest } as RedirectRequest);
    } else {
      this.authService.loginRedirect();
    }
  }

  loginPopup(): void {
    if (this.msalGuardConfig.authRequest) {
      this.authService.loginPopup({ ...this.msalGuardConfig.authRequest } as PopupRequest)
        .subscribe((response: AuthenticationResult) => {
          this.authService.instance.setActiveAccount(response.account);
          this.setLoginDisplay(); // Actualizar el estado después del login
        });
    } else {
      this.authService.loginPopup()
        .subscribe((response: AuthenticationResult) => {
          this.authService.instance.setActiveAccount(response.account);
          this.setLoginDisplay();
        });
    }
  }

  logout(popup?: boolean): void {
    if (popup) {
      this.authService.logoutPopup({ mainWindowRedirectUri: "/" });
    } else {
      this.authService.logoutRedirect();
    }
    this.userProfile = null; 

  }

  ngOnDestroy(): void {
    this._destroying$.next();
    this._destroying$.complete();
  }

  toggleLogin(): void {
    this.isLoggingToggled = !this.isLoggingToggled;

  }

  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;

  }
}