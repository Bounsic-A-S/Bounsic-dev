import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { LucideAngularModule, ChevronLeft } from 'lucide-angular';
import { TranslateModule } from '@ngx-translate/core';
@Component({
  selector: 'app-user-settings',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    LucideAngularModule,
    TranslateModule
  ],
  templateUrl: './settings.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsComponent {
  readonly leftArrow = ChevronLeft;

  constructor(private router: Router) { }

  goBack(): void {
    this.router.navigate(['/dashboard']);
  }

  menuItems = [
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.ACCOUNT', route: 'account' },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.PRIVACY' },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.CONNECTIONS' },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.NOTIFICATIONS' },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.PLAN' },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.PLAYER' },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.PREFERENCES', route: 'appearance' },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.LANGUAGE', route: 'language' }
  ];

}
