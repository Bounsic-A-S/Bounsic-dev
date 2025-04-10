import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
@Component({
  selector: 'app-user-settings',
  standalone: true,
  imports: [
    CommonModule,
  ],
  templateUrl: './settings.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class SettingsComponent {
}
