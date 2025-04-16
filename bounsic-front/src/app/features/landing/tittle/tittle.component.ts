// smooth-hover-text.component.ts
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { TranslateModule } from '@ngx-translate/core';
@Component({
  selector: 'app-landing-tittle',
  templateUrl: './tittle.component.html',
  styleUrls: ['./tittle.component.css'],
  imports: [TranslateModule],
  standalone: true,
  changeDetection: ChangeDetectionStrategy.OnPush,
  
})
export class LandingTextComponent {
  isHovered: boolean = false;

  onHover() {
    this.isHovered = true;
  }

  onLeave() {
    this.isHovered = false;
  }
}