import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { Router } from '@angular/router';
import { NotFoundButtonComponent } from './button/404_button.component';
import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';

@Component({
  selector: 'app-router-err',
  standalone: true,
  templateUrl: './404.component.html',
  styleUrl: './404.component.css',
  imports: [CommonModule, NotFoundButtonComponent],
  changeDetection: ChangeDetectionStrategy.OnPush,
  schemas: [CUSTOM_ELEMENTS_SCHEMA] // for web components function props

})
export class NotFoundComponent {
  constructor(private readonly router: Router) { }

  redirectToDashboard = (): void => {
    this.router.navigate(['/']);
  }
}
