import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import { AuthService } from '@app/services/auth/auth.service';
import { UserService } from '@app/services/auth/user.service';
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
  private theme: string = 'dark';
  public customThemeSelected: string =
    localStorage.getItem('background') ?? 'bg-bounsic-gradient';
  public customThemes = [
    {
      bounsic: [
        { name: 'bg-bounsic-gradient', isLight: false },
        { name: 'bg-bounsic-custom-gradient-blue', isLight: false },
        { name: 'bg-bounsic-custom-gradient-purple', isLight: false },
      ],
      gradient: [{ name: 'bg-bounsic-gradient-about-mobile', isLight: false }],
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
    if (user) {
      id = user.id_user;
    }
    console.log(user);
    if (id === 0) return;
    this.userService.setBackground(this.customThemeSelected, id).subscribe({
      next: () => {
        console.log('BG updated successfully');
      },
      error: (error) => {
        console.error('Error updating BG:', error);
      },
    });
    localStorage.setItem('background', this.customThemeSelected);
  }
}
