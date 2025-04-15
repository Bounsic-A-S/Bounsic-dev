import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { LucideAngularModule, ChevronLeft } from 'lucide-angular';

@Component({
  selector: 'app-user-settings',
  standalone: true,
  imports: [
    CommonModule, 
    RouterModule,
    LucideAngularModule
  ],
  templateUrl: './settings.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsComponent {
  public leftArrow = ChevronLeft;

  constructor(private router: Router) {}

  goBack(): void {
    this.router.navigate(['/dashboard']);
  }

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
