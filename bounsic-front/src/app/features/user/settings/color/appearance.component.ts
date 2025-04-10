import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'user-settings-appearance',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './appearance.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsAppearanceComponent {
}
