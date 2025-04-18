import { ChangeDetectionStrategy, Component, HostListener } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { LucideAngularModule, ChevronLeft, Menu } from 'lucide-angular';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-user-settings',
  standalone: true,
  imports: [
    CommonModule,
    RouterModule,
    LucideAngularModule,
    TranslateModule,
    ClickOutsideDirective
  ],
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
