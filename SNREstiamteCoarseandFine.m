

%% Test signal
fs = 48e3;
fc = 2500 - 17;
ts = 1/fs;
N = 5*10^3;
rand_phase = 2*pi*randn(1,1);
IQ_val = sin(2*pi*fc*ts*(1:N)+rand_phase) + 0.08*randn(1,N);



%%
IQ_val = read_file('SIgnGenTRansmit900pt05_minus56pt5dBm1sec_trial1.bin');
offset=1e5;
IQ_val = IQ_val((1:10^3)+offset);
fc = 50e3;
fs = 2.5e6;
% fs = 1.25e6;
ts = 1/fs;
% IQ_val = read_file('.bin');
N = length(IQ_val);

IQ_real = real(IQ_val);
IQ_imag = imag(IQ_val);

IQ_real_norm = IQ_real/max(IQ_real);
IQ_real_norm =IQ_real_norm';
IQ_imag_norm = IQ_imag/max(IQ_imag);
IQ_imag_norm = IQ_imag_norm';
amp_start = 0.8;
amp_end = 1.2;
amp_step = 0.05; %0.01
freq_start = fc-200;
freq_end = fc+200;
freq_step = 20; %0.2
phase_start = 0;
phase_step = 2*pi/10; %2*pi/360
phase_end = 2*pi;
i=0;
len1 = length(amp_start:amp_step:amp_end);
len2 = length(freq_start:freq_step:freq_end);
len3 = length(phase_start:phase_step:phase_end);
real_error_val = zeros(len1,len2,len3);
imag_error_val = zeros(len1,len2,len3);
real_error_val_fine = zeros(len1,len2,len3);
imag_error_val_fine = zeros(len1,len2,len3);
for a_val = amp_start:amp_step:amp_end
    i=i+1
    j=0;
   for freq_val=freq_start:freq_step:freq_end
       j=j+1;
       k=0;
      for phase_val = phase_start:phase_step:phase_end
         k=k+1;
         %a_val
         signal_estimate = a_val*cos(2*pi*freq_val*ts*[1:N] + phase_val);
         real_error_val(i,j,k) = mean((IQ_real_norm - signal_estimate).^2);
         imag_error_val(i,j,k) = mean((IQ_imag_norm - signal_estimate).^2);
      end
   end
end


[mxv_real,idx] = min(real_error_val(:));
[i_real,j_real,k_real] = ind2sub(size(real_error_val),idx);

[mxv_imag,idx] = min(imag_error_val(:));
[i_imag,j_imag,k_imag] = ind2sub(size(imag_error_val),idx);


amp_range = amp_start:amp_step:amp_end;
freq_range = freq_start:freq_step:freq_end;
phase_range = phase_start:phase_step:phase_end;


true_amp_real_coarse = amp_range(i_real)
true_freq_real_coarse = freq_range(j_real)
true_phase_real_coarse = phase_range(k_real)

% Fine search

amp_start = true_amp_real_coarse-0.07;
amp_end = true_amp_real_coarse+0.07;
amp_step = 0.005; %0.01
freq_start = true_freq_real_coarse-30;
freq_end = true_freq_real_coarse+30;
freq_step = 1; %0.2
phase_start = true_phase_real_coarse - 2*pi/10;
phase_step = 2*pi/360; %2*pi/360
phase_end = true_phase_real_coarse + 2*pi/10;

i=0;
for a_val = amp_start:amp_step:amp_end
    i=i+1
    j=0;
   for freq_val=freq_start:freq_step:freq_end
       j=j+1;
       k=0;
      for phase_val = phase_start:phase_step:phase_end
         k=k+1;
         %a_val
         signal_estimate = a_val*cos(2*pi*freq_val*ts*[1:N] + phase_val);
         real_error_val_fine(i,j,k) = mean((IQ_real_norm - signal_estimate).^2);
         %imag_error_val_fine(i,j,k) = mean((IQ_imag_norm - signal_estimate).^2);
      end
   end
end



%

[mxv_real,idx] = min(real_error_val_fine(:));
[i_real_fine,j_real_fine,k_real_fine] = ind2sub(size(real_error_val_fine),idx);

%[mxv_imag,idx] = min(imag_error_val_fine(:));
%[i_imag_fine,j_imag_fine,k_imag_fine] = ind2sub(size(imag_error_val_fine),idx);

amp_range = amp_start:amp_step:amp_end;
freq_range = freq_start:freq_step:freq_end;
phase_range = phase_start:phase_step:phase_end;


true_amp_real_fine = amp_range(i_real_fine)
true_freq_real_fine = freq_range(j_real_fine)
true_phase_real_fine = phase_range(k_real_fine)

real_fine_signal_estimate = true_amp_real_fine*cos(2*pi*true_freq_real_fine*ts*[1:N] + true_phase_real_fine);
%imag_best_signal_estimate = amp_range(i_imag)*cos(2*pi*freq_range(j_imag)*ts*[1:N] + phase_range(k_imag));


% error_signal_real = IQ_real_norm - real_best_signal_estimate;
SNR_estimate_real = 10*log10(mean((real_fine_signal_estimate).^2)/mxv_real)
%SNR_estimate_imag = 10*log10(mean((imag_best_signal_estimate).^2)/mxv_imag)

