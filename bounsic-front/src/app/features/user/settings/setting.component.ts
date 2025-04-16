import { ChangeDetectionStrategy, Component, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { LucideAngularModule, ChevronLeft, Menu } from 'lucide-angular';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';

@Component({
  selector: 'app-user-settings',
  standalone: true,
  imports: [CommonModule, RouterModule, LucideAngularModule, ClickOutsideDirective],
  templateUrl: './settings.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsComponent {
  public leftArrow = ChevronLeft;
  public menuIcon = Menu;

  constructor(private router: Router) {}

  public sideBarOpen = true;

  goBack(): void {
    this.router.navigate(['/dashboard']);
  }

  toggleSidebar(): void {
    this.sideBarOpen = !this.sideBarOpen;
  }
  closeSideBar(): void {
    if(window.innerWidth < 768){
      this.sideBarOpen = false;
    }
  }
  @HostListener('window:resize', ['$event'])
  onResize(event: any): void {
    this.sideBarOpen = event.target.innerWidth > 768;
  }


  menuItems = [
    { label: 'Account', route: 'account' },
    { label: 'Privacidad' },
    { label: 'Conexiones' },
    { label: 'Notificaciones' },
    { label: 'Plan' },
    { label: 'Reproducción' },
    { label: 'Apariencia', route: 'appearance' },
    { label: 'Idioma', route: 'language' },
  ];
}
