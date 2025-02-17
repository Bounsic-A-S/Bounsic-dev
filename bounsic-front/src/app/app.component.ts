import { ChangeDetectionStrategy, Component } from '@angular/core';
import { LandingComponent } from './features/landing/landing.component';

@Component({
  selector: 'app-root', // name of the component
  standalone: true, // not module
  templateUrl: './app.component.html', // render
  imports: [LandingComponent], // imports what we need
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent { }
