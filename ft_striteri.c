/* ************************************************************************** */
/*                                                                            */
/*                                                        :::      ::::::::   */
/*   ft_striteri.c                                      :+:      :+:    :+:   */
/*                                                    +:+ +:+         +:+     */
/*   By: mel-shdo <mustafa.el-shdouh@student.42.    +#+  +:+       +#+        */
/*                                                +#+#+#+#+#+   +#+           */
/*   Created: 2025/12/11 20:41:03 by mel-shdo          #+#    #+#             */
/*   Updated: 2025/12/11 20:47:04 by mel-shdo         ###   ########.fr       */
/*                                                                            */
/* ************************************************************************** */

#include "libft.h"
//#include <stdio.h>
//#include <ctype.h>

void	ft_striteri(char *s, void (*f)(unsigned int, char*))
{
	unsigned int	i;

	i = 0;
	if (!s || !f)
		return ;
	while (s[i])
	{
		f(i, &s[i]);
		i++;
	}
}

/*void	my_iter_func(unsigned int i, char *c)
{
	// Example: capitalize only characters at even indices
	if (i % 2 == 0)
		*c = toupper(*c);
}

int	main(void)
{
	// NOTE: We must use a mutable array, not a string literal!
	// char *str = "hello"; -> This effectively is read-only memory -> SEGFAULT
	char	str[] = "hello world"; 

	printf("Before: %s\n", str);

	ft_striteri(str, my_iter_func);

	printf("After : %s\n", str); // Expected: "HeLlO WoRlD"
	
	return (0);
}*/