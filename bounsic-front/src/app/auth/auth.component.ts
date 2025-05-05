import {
  ChangeDetectionStrategy,
  Component,
  EventEmitter,
  Input,
  Output,
  inject
} from '@angular/core';
import { CommonModule } from '@angular/common';
import {
  FormBuilder,
  FormGroup,
  ReactiveFormsModule,
  Validators
} from '@angular/forms';
import { AuthService } from '@app/services/auth/auth.service';
import { ClickOutsideDirective } from '@app/directive/clickoutside.directive';
import { TranslateModule } from '@ngx-translate/core';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule, ClickOutsideDirective, TranslateModule],
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})
export class AuthComponent {
  @Input() isOpen = false;
  @Output() closeModal = new EventEmitter<void>();

  isRegisterForm = true;
  isSubmitting = false;
  registerForm: FormGroup;

  private fb = inject(FormBuilder);
  private authService = inject(AuthService);

  constructor() {
    this.registerForm = this.fb.group({
      username: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
    });
  }

  close(): void {
    this.closeModal.emit();
  }

  toggleForms(): void {
    this.isRegisterForm = !this.isRegisterForm;
    if (!this.isRegisterForm) {
      this.registerForm.reset();
    }
  }

  onLogin(): void {
    if (this.isRegisterForm) {
      // Microsoft login
      this.authService
        .loginPopup()
        .then((response) => {
          console.log('MS Login Success:', response);
          this.close();
        })
        .catch((error) => {
          console.error('MS Login Error:', error);
        });
    } else {
      if (this.registerForm.invalid) {
        Object.keys(this.registerForm.controls).forEach((key) => {
          this.registerForm.get(key)?.markAsTouched();
        });
        return;
      }

      this.isSubmitting = true;
      const formValues = this.registerForm.value;
      const formData = new FormData();
      formData.append('username', formValues.username);
      formData.append('email', formValues.email);

      setTimeout(() => {
        console.log('Registration data:', {
          username: formValues.username,
          email: formValues.email,
        });
        this.isSubmitting = false;
        this.isRegisterForm = true;
        this.registerForm.reset();
      }, 1000);
    }
  }
}
