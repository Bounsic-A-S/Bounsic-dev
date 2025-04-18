import {
  ChangeDetectionStrategy,
  Component,
  OnInit,
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
  isMobileMenuOpen = false;
  userProfile: any = null;
  isLoggingToggled = false;
  //icons
  readonly Heart = Heart;
  readonly loginIcon = LogIn;
  readonly logoutIcon = LogOut;
  readonly settingsIcon = Settings;

  constructor(
    private authService: AuthService,
    private router: Router
  ) {}

  isModalOpen = false; // Controla si el modal está abierto o cerrado

  ngOnInit(): void {
    this.authService.initialize()
  }
  goToSettings() {
    this.router.navigate(['/settings']);
  }
  isUserLogged(){
    this.userProfile = this.authService.getUserProfile()
    return this.userProfile !== null
  }
  openModal() {
    this.isModalOpen = true; // Abre el modal
  }
  closeModal() {
    this.isModalOpen = false; // Cierra el modal
  }
  logout():void{
    this.authService.logout(true);
    this.userProfile = this.authService.getUserProfile();
  }
  toggleLogin(): void {
    this.isLoggingToggled = !this.isLoggingToggled;
  }
  toggleMobileMenu(): void {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }
}
