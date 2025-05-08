import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { AuthService } from '@app/services/auth/auth.service';
import { UserService } from '@app/services/auth/user.service';
import { BackgroundService } from '@app/services/background.service';
@Component({
  selector: 'user-settings-appearance',
  standalone: true,
  imports: [CommonModule, TranslateModule],
  templateUrl: './appearance.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsAppearanceComponent {
  private authService = inject(AuthService);
  private userService = inject(UserService);
  private backgroundService = inject(BackgroundService)
  private theme: string = localStorage.getItem('theme') ?? 'dark';
  public customThemeSelected: string =
    localStorage.getItem('background') ?? 'bg-bounsic-gradient';
  public customThemes = [
    {
      bounsic: [
        { name: 'bg-bounsic-gradient', isLight: false },
        { name: 'bg-bounsic-custom-gradient-blue', isLight: false },
        { name: 'bg-bounsic-custom-gradient-purple', isLight: false },
        { name: 'bg-bounsic-custom-gradient-white', isLight: true },

      ],
      gradient: [
        { name: 'bg-bounsic-gradient-about-mobile', isLight: false },
        { name: 'bg-bounsic-custom-gradient-pink-based', isLight: true },
        { name: 'bg-bounsic-custom-gradient-blue-based', isLight: false },
        { name: 'bg-bounsic-custom-gradient-orange-purple-based', isLight: false },
        { name: 'bg-bounsic-custom-gradient-red-based', isLight: false },
        { name: 'bg-bounsic-custom-gradient-green-based', isLight: false },
      ],
      solid: [
        { name: 'bg-bounsic-red', isLight: true },
        { name: 'bg-bounsic-yellow', isLight: true },
      ],
    },
  ];

  toggleTheme(theme: string): void {
    this.theme = theme;
  }

  private getTheme(): string {
    return this.theme;
  }
  isLightTheme(): boolean {
    return this.getTheme() === 'light';
  }
  setCustomTheme(theme: string): void {
    this.customThemeSelected = theme;
  }
  hasThemeChange(): boolean {
    const actualTheme = localStorage.getItem('background');
    return actualTheme !== this.customThemeSelected;
  }
  saveTheme(): void {
    const user = this.authService.getUserProfile();
    let id = 0;
    if (user) id = user.id_user;
    if (id === 0) return;
    const data = {
      background: this.customThemeSelected,
      theme: this.theme
    }
    this.userService.setBackground(data, id).subscribe({
      error: (error) => {
        console.error('Error updating BG & theme:', error);
      },
    });
    this.backgroundService.setBackground(this.customThemeSelected);

    if (this.theme !== localStorage.getItem('theme')) {
      document.documentElement.className = '';
      document.documentElement.classList.add(this.theme);
      localStorage.setItem('theme', this.theme);
    }
  }
}
