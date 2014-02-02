# libs/utils.py
import re

def extract_hashtags(s):
	return set([re.sub(r"(\W+)$", "", j) for j in set([i for i in s.split() if i.startswith("#")])])

def get_or_none(model, **kwargs):
    try:
        return model.objects.get(**kwargs)
    except model.DoesNotExist:
        return None

def phone_format(n):
	try:
		return format(int(n[:-1]), ",").replace(",", "-") + n[-1]
	except ValueError:
		return None