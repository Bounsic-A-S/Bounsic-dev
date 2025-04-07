import { ChangeDetectionStrategy, Component, ElementRef, EventEmitter, Input, Output, ViewChild } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormBuilder, FormGroup, ReactiveFormsModule, Validators } from '@angular/forms';

@Component({
  selector: 'app-auth',
  standalone: true,
  imports: [CommonModule, ReactiveFormsModule],
  templateUrl: './auth.component.html',
  styleUrls: ['./auth.css'],
  changeDetection: ChangeDetectionStrategy.OnPush,
})

export class AuthComponent {
  @Input() isOpen = false;
  @Output() closeModal = new EventEmitter<void>();
  @ViewChild('fileInput') fileInput!: ElementRef;
  
  isRegisterForm = true;
  isSubmitting = false;
  
  // Image preview property
  imagePreview: string | ArrayBuffer | null = null;
  
  // Add the register form
  registerForm: FormGroup;
  
  constructor(private fb: FormBuilder) {
    // Initialize register form with all required fields including the image
    this.registerForm = this.fb.group({
      name: ['', [Validators.required]],
      last_name: ['', [Validators.required]],
      email: ['', [Validators.required, Validators.email]],
      password: ['', [Validators.required, Validators.minLength(8)]],
      profileImage: [null]
    });
  }
  
  get selectedFileName(): string {
    const file = this.registerForm.get('profileImage')?.value;
    return file ? file.name : '';
  }
  
  close(): void {
    this.closeModal.emit();
  }
  
  toggleForms(): void {
    this.isRegisterForm = !this.isRegisterForm;
    if (!this.isRegisterForm) {
      this.registerForm.reset();
      this.imagePreview = null;
    }
  }
  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      const file = input.files[0];
      
      // Update the form control with the file
      this.registerForm.patchValue({
        profileImage: file
      });
      
      // Mark the control as touched to trigger validation
      this.registerForm.get('profileImage')?.markAsTouched();
      
      // Create a preview of the image
      const reader = new FileReader();
      reader.onload = () => {
        this.imagePreview = reader.result;
      };
      reader.readAsDataURL(file);
    }
  }
  
  removeImage(): void {
    // Reset the form control
    this.registerForm.patchValue({
      profileImage: null
    });
    
    this.imagePreview = null;
    if (this.fileInput) {
      this.fileInput.nativeElement.value = '';
    }
  }
  
  onLogin(): void {
    // Keep existing login logic
    if (this.isRegisterForm) {
      // Original login logic
      console.log('Login clicked');
    } else {
      // Handle registration
      if (this.registerForm.invalid) {
        // Mark all fields as touched to trigger validation messages
        Object.keys(this.registerForm.controls).forEach(key => {
          this.registerForm.get(key)?.markAsTouched();
        });
        return;
      }
      
      this.isSubmitting = true;
      
      // Get form values including the file
      const formValues = this.registerForm.value;
      
      // Create FormData object for API submission
      const formData = new FormData();
      formData.append('name', formValues.name);
      formData.append('last_name', formValues.last_name);
      formData.append('email', formValues.email);
      formData.append('password', formValues.password);
      
      if (formValues.profileImage) {
        formData.append('profile_image', formValues.profileImage, formValues.profileImage.name);
      }
      
      // Simulate registration API call
      setTimeout(() => {
        console.log('Registration data:', {
          name: formValues.name,
          last_name: formValues.last_name,
          email: formValues.email,
          hasImage: !!formValues.profileImage,
          imageName: formValues.profileImage ? formValues.profileImage.name : 'No image selected'
        });
        this.isSubmitting = false;
        this.isRegisterForm = true; // Switch back to login after registration
        this.registerForm.reset();
        this.imagePreview = null;
      }, 1000);
    }
  }
}