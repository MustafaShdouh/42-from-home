/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_strmapi.c                                       :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mel-shdo@learner.42.tech>        +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/12 17:42:46 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/12 17:43:00 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

//#include <stddef.h>
#include <stdlib.h>
//#include <ctype.h>
//#include <stdio.h>
//#include <string.h>

char	*ft_strmapi(char const *s, char (*f)(unsigned int, char))
{
	unsigned int	i;
	char			*str;

	i = 0;
	if (!s || !f)
		return (NULL);
	str = (char *)malloc(sizeof(char) * (ft_strlen(s) + 1));
	if (!str)
		return (NULL);
	while (s[i])
	{
		str[i] = f(i, s[i]);
		i++;
	}
	str[i] = '\0';
	return (str);
}

/*char	my_func(unsigned int i, char c)
{
	if (i % 2 == 0)
		return (toupper(c));
	return (c);
}

int	main(void)
{
	char	*str = "hello world";
	char	*result;

	printf("Original: %s\n", str);
	result = ft_strmapi(str, my_func);

	if (result)
	{
		printf("Modified: %s\n", result);
		free(result);
	}
	else
	{
		printf("Allocation failed\n");
	}

	return (0);
}*/