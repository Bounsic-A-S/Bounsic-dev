import { ChangeDetectionStrategy, Component, HostListener, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule, Router } from '@angular/router';
import { LucideAngularModule, ChevronLeft, Menu, UserRoundPen, Lock, Workflow, MessageSquare, Palette, Languages, AudioLines } from 'lucide-angular';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';
import { TranslateModule } from '@ngx-translate/core';
import { BackgroundService } from '@app/services/background.service';

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

  readonly leftArrow = ChevronLeft;
  readonly menuIcon = Menu;
  // icons for settings
  readonly account = UserRoundPen;
  readonly privacy = Lock;
  readonly connections = Workflow;
  readonly notifications = MessageSquare;
  readonly player = AudioLines;
  readonly preferences = Palette;
  readonly language = Languages;

  constructor(private router: Router) {}
  private backgroundService = inject(BackgroundService)
  public sideBarOpen = true;
  bg$ = this.backgroundService.background$

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
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.ACCOUNT', route: 'account', icon: this.account },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.PRIVACY', icon: this.privacy },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.CONNECTIONS',icon: this.connections },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.NOTIFICATIONS',icon: this.notifications },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.PLAYER', icon: this.player },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.PREFERENCES', route: 'appearance', icon: this.preferences },
    { label: 'BOUNSIC.SETTINGS.SIDEBAR.LANGUAGE', route: 'language', icon: this.language },
  ];
}
