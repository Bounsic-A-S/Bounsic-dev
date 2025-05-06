import { CommonModule } from '@angular/common';
import { ChangeDetectionStrategy, Component, Input } from '@angular/core';

@Component({
    selector: 'router-err-button',
    standalone: true,
    templateUrl: './404_button.component.html',
    imports: [CommonModule],
    changeDetection: ChangeDetectionStrategy.OnPush

})
export class NotFoundButtonComponent {
    @Input() redirectToDashboard!: () => void;
}
