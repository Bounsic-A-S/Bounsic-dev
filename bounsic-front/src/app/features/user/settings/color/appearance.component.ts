import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
@Component({
  selector: 'user-settings-appearance',
  standalone: true,
  imports: [
    CommonModule,
    TranslateModule
  ],
  templateUrl: './appearance.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsAppearanceComponent {
  private theme : string = 'dark';
  public customThemeSelected: string = localStorage.getItem('background') ?? 'bg-bounsic-gradient';
  public customThemes = [
    {
      bounsic: [
        { name: 'bg-bounsic-gradient', isLight: false },
        { name: 'bg-bounsic-custom-gradient-blue', isLight: false },
        { name: 'bg-bounsic-custom-gradient-purple', isLight: false },
      ],
      gradient: [
        { name: 'bg-bounsic-gradient-about-mobile', isLight: false }
      ],
      solid: [
        { name: 'bg-bounsic-red', isLight: true },
        { name: 'bg-bounsic-yellow', isLight: true }

      ]
    }
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
}
