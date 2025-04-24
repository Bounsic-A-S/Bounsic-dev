import { ChangeDetectionStrategy, Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { LucideAngularModule } from 'lucide-angular';
import { TranslateModule, TranslateService } from '@ngx-translate/core';

@Component({
  selector: 'user-settings-language',
  standalone: true,
  imports: [CommonModule, RouterModule, LucideAngularModule, TranslateModule],
  templateUrl: './language.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LanguageComponent {
  private translateService = inject(TranslateService);
  public actualLang = localStorage.getItem('language') || 'es';

  changeLanguage(event: Event) {
    if (event.target) {
      const changeEvent = event.target as HTMLInputElement;
      this.translateService.use(changeEvent.value);
      localStorage.setItem('language', changeEvent.value);
    }
  }
}
