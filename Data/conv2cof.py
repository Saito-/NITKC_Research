# coding: shift-jis
# conv2cof.py
# �R�[�h�i�s���ܓx���Ɋ�Â��Đ��l������

import math
from itertools import chain

# ���F�̃��X�g
tone = ['C', 'C#', 'D', 'D#', 'E', 'F', 'F#', 'G', 'G#', 'A', 'A#', 'B']
tone2num = { v:k for k, v in enumerate(tone) }

# �ܓx����ł̎剹�̕��� (���W���[)
cof = ['C', 'G', 'D', 'A', 'E', 'B', 'F#', 'C#', 'G#', 'D#', 'A#', 'F']
cof2num = { v:k for k, v in enumerate(cof) }

# �ܓx����ł̎剹�̕��� (�}�C�i�[)
cof_minor = ['Am', 'Em', 'Bm', 'F#m', 'C#m', 'G#m', 'D#m', 'A#m', 'Fm', 'Cm', 'Gm', 'Dm']
cof_minor2num = { v:k for k, v in enumerate(cof_minor)}

# suffix �𐔒l�ɕϊ�����
suffix2num = {
	'm7-5'  :  1,
	'm7'    :  2,
	'mM7'   :  3,
	'm6'    :  4,
	'dim'   :  5,
	'm'     :  6,
	'sus4'  :  8,
	'aug'   :  9,
	'add9'  : 10,
	'6'     : 11,
	'7'     : 12,
	'M7'    : 13,
	'7sus4' : 14,
	'9'     : 15,
}

# �J�|�̏��Ɋ�Â��ăR�[�h�i�s���V�t�g����
def shift_tone(t, capo, shift):
	tn = tone2num[t]
	on = (tn + capo) % 12
	idx = (on - shift) % 12
	return tone[idx]

# �R�[�h�i�s�𐔒l������
def to_cof(chords, keys):
	while True:
		try:
			chords.remove('')
		except:
			break
	ret = []
	suffix_m = [
		'm7-5', 
		'mM7', 'dim',
		'm6', 'm7',
		'm',
	]

	suffix_M = [
		'7sus4', 
		'sus4', 'add9', 
		'aug',
		'M7',
		'6', '7','9',
	]

	origin, capo, play = keys
	capo = int(capo)

	if 'm' in origin:
		shift = tone2num[origin.split('m')[0]]
	else:
		shift = tone2num[origin]
	shift=0
	for chord in chords:
		flg = False
		for i in xrange(len(suffix_m)):
			s = suffix_m[i]
			if s in chord:
				t = chord.split(s)[0]
				shifted = shift_tone(t, capo, shift) + 'm'
				r = suffix2num[s]
				theta = cof_minor2num[shifted]
				dat = (0, theta)
				ret.append(dat)
				flg = True
				break
		if flg: continue
		for i in xrange(len(suffix_M)):
			s = suffix_M[i]
			if s in chord:
				t = chord.split(s)[0]
				shifted = shift_tone(t, capo, shift)
				r = suffix2num[s]
				theta = cof2num[shifted]
				dat = (1, theta)
				ret.append(dat)
				flg = True
				break
		if flg: continue
		t = chord
		shifted = shift_tone(t, capo, shift)
		theta = cof2num[shifted]
		dat = (1, theta)
		ret.append(dat)
	return ret

# �ȍ��W�����[�N���b�h���W�ɕϊ�����
def convpolar2euc(chords):
	ret = []
	for chord in chords:
		x = chord[1] * math.cos(chord[0])
		y = chord[1] * math.sin(chord[0])
		dat = (x, y)
		ret.append(dat)
	return ret
