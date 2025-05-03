import { ChangeDetectionStrategy, Component, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
import User from 'src/types/user/User';
import { AuthService } from '@app/services/auth/auth.service';
@Component({
  selector: 'user-settings-account',
  standalone: true,
  imports: [
    CommonModule,
    TranslateModule
  ],
  templateUrl: './account.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsAccountComponent implements OnInit {
  private authService = inject(AuthService);
  user: User | null = null;

  ngOnInit(): void {
    this.user = this.authService.getUserProfile()
  }
}
