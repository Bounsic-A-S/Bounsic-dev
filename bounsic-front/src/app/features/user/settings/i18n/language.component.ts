import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { LucideAngularModule } from 'lucide-angular';
import { TranslateModule, TranslateService } from '@ngx-translate/core';
import { UserService } from '@app/services/auth/user.service';
import { AuthService } from '@app/services/auth/auth.service';

@Component({
  selector: 'user-settings-language',
  standalone: true,
  imports: [CommonModule, RouterModule, LucideAngularModule, TranslateModule],
  templateUrl: './language.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LanguageComponent {
  private translateService = inject(TranslateService);
  private userService = inject(UserService);
  private authService = inject(AuthService);
  public actualLang = localStorage.getItem('language') || 'es';

  changeLanguage(event: Event) {
    if (event.target) {
      const changeEvent = event.target as HTMLInputElement;
      this.translateService.use(changeEvent.value);
      localStorage.setItem('language', changeEvent.value);
      this.saveLanguage(changeEvent.value);
    }
  }
  private saveLanguage(language: string): void {
    const user = this.authService.getUserProfile();
    let id = 0;
    if (user) {
      id = user.id_user;
    }
    console.log(user)
    if(id === 0) return
    this.userService.setLanguage(language,id ).subscribe({
      next: () => {
        console.log('Language updated successfully');
      },
      error: (error) => {
        console.error('Error updating language:', error);
      },
    });
  }
}
