import { ChangeDetectionStrategy, Component } from '@angular/core';
import { LandingTextComponent } from './tittle/tittle.component';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [LandingTextComponent],
  templateUrl: './landing.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LandingComponent {}
