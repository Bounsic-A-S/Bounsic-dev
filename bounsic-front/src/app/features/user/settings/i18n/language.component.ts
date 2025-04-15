import { ChangeDetectionStrategy, Component } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { LucideAngularModule } from 'lucide-angular';

@Component({
    selector: 'user-settings-language',
    standalone: true,
    imports: [
        CommonModule,
        RouterModule,
        LucideAngularModule
    ],
    templateUrl: './language.component.html',
    changeDetection: ChangeDetectionStrategy.OnPush,
})
export class LanguageComponent {
}
