import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { TranslateModule } from '@ngx-translate/core';
@Component({
  selector: 'user-settings-appearance',
  standalone: true,
  imports: [
    CommonModule,
    TranslateModule
  ],
  templateUrl: './appearance.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsAppearanceComponent {
}
