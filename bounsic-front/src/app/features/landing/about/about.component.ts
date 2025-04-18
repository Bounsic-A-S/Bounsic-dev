
import { ChangeDetectionStrategy, Component } from '@angular/core';
import { Router } from '@angular/router';
import { LandingNavBarComponent } from '@app/features/landing/navbar/navbar.component';
import { TranslateModule } from '@ngx-translate/core';
@Component({
    selector: 'app-about-us', // Nombre del componente
    standalone: true, // No requiere módulo
    templateUrl: './about.component.html', // Vista del componente
    imports: [
      LandingNavBarComponent,
      TranslateModule
    ], 
    changeDetection: ChangeDetectionStrategy.OnPush
})
export class AboutUsComponent { 
    constructor(private  readonly router: Router) {}

    redirectToDashboard(): void {
      this.router.navigate(['/']);
    }
}
