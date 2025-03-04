import { Component } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'main-navbar',
  templateUrl: './navbar-app.component.html',
  standalone: true,
  imports: [CommonModule],
})
export class NavbarAppComponent {
  isMobileMenuOpen = false;
  isLoggedIn = false; // Simulated authentication state
  isLoggingToggled = false;

  constructor(readonly router: Router) {}

  toggleMobileMenu() {
    this.isMobileMenuOpen = !this.isMobileMenuOpen;
  }
  toggleLogin(){
    this.isLoggingToggled =!this.isLoggingToggled;
  }

  login() {
    this.isLoggedIn = true;
    this.router.navigate(['/dashboard']);
  }

  logout() {
    this.isLoggedIn = false;
    this.router.navigate(['/']);
  }
}
