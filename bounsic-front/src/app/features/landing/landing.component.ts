import { ChangeDetectionStrategy, Component } from '@angular/core';
import { LandingTextComponent } from './tittle/tittle.component';
import { LandingNavBarComponent } from './navbar/navbar.component';

@Component({
  selector: 'app-landing',
  standalone: true,
  imports: [LandingTextComponent,LandingNavBarComponent],
  templateUrl: './landing.component.html',
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class LandingComponent {}
