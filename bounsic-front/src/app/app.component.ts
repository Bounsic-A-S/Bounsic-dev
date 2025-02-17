import { ChangeDetectionStrategy, Component } from '@angular/core';
import {RouterModule} from '@angular/router';
import { NavbarComponent } from './shared/components/navbar/navbar.component';

@Component({
  selector: 'app-root', // name of the component
  standalone: true, // not module
  templateUrl: './app.component.html', // render
  imports: [RouterModule,NavbarComponent], // imports what we need
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent { }
