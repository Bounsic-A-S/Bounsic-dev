import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
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
export class SettingsAccountComponent {
}
