import { ComponentFixture, TestBed } from '@angular/core/testing';
import { NavbarAppComponent } from '@app/shared/navbar/navbar-app.component';
import { MsalService, MsalBroadcastService, MSAL_GUARD_CONFIG } from '@azure/msal-angular';
import { provideRouter, withComponentInputBinding } from '@angular/router';
import { of, Subject } from 'rxjs';
import { PLATFORM_ID } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
describe('NavbarAppComponent', () => {
  let component: NavbarAppComponent;
  let fixture: ComponentFixture<NavbarAppComponent>;

  const mockMsalService = {
    handleRedirectObservable: () => of(),

    instance: {
      getAllAccounts: () => [],
      setActiveAccount: () => { },
      enableAccountStorageEvents: () => { },
      getActiveAccount: () => null,
    }
  };

  const mockMsalBroadcastService = {
    msalSubject$: new Subject(),
    inProgress$: of()
  };

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [NavbarAppComponent,TranslateModule.forRoot()],
      providers: [
        { provide: PLATFORM_ID, useValue: 'browser' },
        { provide: MsalService, useValue: mockMsalService },
        { provide: MsalBroadcastService, useValue: mockMsalBroadcastService },
        { provide: MSAL_GUARD_CONFIG, useValue: {} },
        provideRouter([], withComponentInputBinding()),

      ]
    }).compileComponents();

    fixture = TestBed.createComponent(NavbarAppComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create the navbar', () => {
    expect(component).toBeTruthy();
  });

  it('should toggle mobile menu', () => {
    expect(component.isMobileMenuOpen).toBeFalse();
    component.toggleMobileMenu();
    expect(component.isMobileMenuOpen).toBeTrue();
    component.toggleMobileMenu();
    expect(component.isMobileMenuOpen).toBeFalse();
  });

  it('should toggle the login option', () => {
    expect(component.isLoggingToggled).toBeFalse();
    component.toggleLogin();
    expect(component.isLoggingToggled).toBeTrue();
    component.toggleLogin();
    expect(component.isLoggingToggled).toBeFalse();
  });
});
