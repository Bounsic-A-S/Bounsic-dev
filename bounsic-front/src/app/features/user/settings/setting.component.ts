import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
@Component({
  selector: 'app-user-settings',
  standalone: true,
  imports: [
    CommonModule, RouterModule,
  ],
  templateUrl: './settings.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsComponent {
  menuItems = [
    { label: 'Account', route: 'account' },
    { label: 'Privacidad' },
    { label: 'Conexiones' },
    { label: 'Notificaciones' },
    { label: 'Plan' },
    { label: 'Reproducción' },
    { label: 'Apariencia', route: 'appearance' },
    { label: 'Idioma' }
  ];

}
