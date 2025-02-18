import { ChangeDetectionStrategy, Component } from '@angular/core';
import {RouterModule} from '@angular/router';

@Component({
  selector: 'app-root', // name of the component
  standalone: true, // not module
  templateUrl: './app.component.html', // render
  imports: [RouterModule], // imports what we need
  changeDetection: ChangeDetectionStrategy.OnPush
})
export class AppComponent { }
