import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { Router } from '@angular/router';
import { TranslateModule } from '@ngx-translate/core';
@Component({
    selector: 'app-404', // Nombre del componente
    standalone: true, // No requiere módulo
    templateUrl: './404.component.html', // Vista del componente
    styleUrls: ['./404.component.css'],
    imports: [CommonModule,TranslateModule], 
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class NotFoundComponent { 
    constructor(private  readonly router: Router) {}

    redirectToDashboard(): void {
      this.router.navigate(['/']);
    }
}
