import {
  ChangeDetectionStrategy,
  Component,
  OnInit,
  inject
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router, RouterModule } from '@angular/router';
import {
  LucideAngularModule,
  LogIn,
  LogOut,
  Heart,
  Settings,
} from 'lucide-angular';
import { AuthComponent } from '@app/auth/auth.component';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';
import { TranslateModule } from '@ngx-translate/core';
import { AuthService } from '@app/services/auth/auth.service';

@Component({
  selector: 'main-navbar',
  templateUrl: './navbar-app.component.html',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    LucideAngularModule,
    AuthComponent,
    ClickOutsideDirective,
    TranslateModule,
  ],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class NavbarAppComponent implements OnInit {
  private authService = inject(AuthService);
  private router = inject(Router);

  isMobileMenuOpen = false;
  userProfile$ = this.authService.userProfile$;
  isLoggingToggled = false;
  isModalOpen = false;

  // Icons
  readonly Heart = Heart;
  readonly loginIcon = LogIn;
  readonly logoutIcon = LogOut;
  readonly settingsIcon = Settings;

  ngOnInit(): void {
    this.authService.initialize();
  }

  goToSettings() {
    this.router.navigate(['/settings']);
  }

  isUserLogged() {
    return this.userProfile$;
  }

  openModal() {
    this.isModalOpen = true;
  }

  closeModal() {
    this.isModalOpen = false;
  }

  logout(): void {
    this.authService.logout(true);
  }

  toggleLogin(): void {
    this.isLoggingToggled = !this.isLoggingToggled;
  }

  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }
}
